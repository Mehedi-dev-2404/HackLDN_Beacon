from functools import lru_cache

from app.core.config import Settings, get_settings
from app.models.persistence.job_repo import JobRepository
from app.models.persistence.task_repo import TaskRepository
from app.services.llm.provider_gemini import GeminiProvider
from app.services.socratic.agent import SocraticAgentService
from app.services.socratic.voice import ElevenLabsVoiceService
from app.services.workflow.pipeline import WorkflowPipeline


@lru_cache(maxsize=1)
def get_cached_settings() -> Settings:
    return get_settings()


@lru_cache(maxsize=1)
def get_job_repo() -> JobRepository:
    settings = get_cached_settings()
    return JobRepository(mongo_uri=settings.mongo_uri, db_name=settings.db_name)


@lru_cache(maxsize=1)
def get_task_repo() -> TaskRepository:
    settings = get_cached_settings()
    return TaskRepository(mongo_uri=settings.mongo_uri, db_name=settings.tasks_db_name)



def get_llm_provider() -> GeminiProvider:
    settings = get_cached_settings()
    return GeminiProvider(
        model=settings.llm_model,
        api_key=settings.gemini_api_key,
        enable_live=settings.enable_live_llm,
    )


@lru_cache(maxsize=1)
def get_socratic_agent() -> SocraticAgentService:
    settings = get_cached_settings()
    return SocraticAgentService(
        model=settings.llm_model,
        api_key=settings.gemini_api_key,
        enable_live=settings.enable_live_llm,
    )


@lru_cache(maxsize=1)
def get_voice_service() -> ElevenLabsVoiceService:
    settings = get_cached_settings()
    return ElevenLabsVoiceService(api_key=settings.eleven_labs_api_key)



def get_workflow_pipeline() -> WorkflowPipeline:
    return WorkflowPipeline(
        job_repo=get_job_repo(),
        task_repo=get_task_repo(),
        llm_provider=get_llm_provider(),
    )
