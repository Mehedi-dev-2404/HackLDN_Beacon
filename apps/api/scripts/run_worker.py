import json

from app.core.dependencies import get_workflow_pipeline



def main() -> None:
    pipeline = get_workflow_pipeline()
    result = pipeline.run(
        source_url="",
        raw_html="<html><body><ul><li>Business Essay Draft</li><li>Math Revision Sheet</li></ul></body></html>",
        scrape_mode="http",
        custom_prompt="Prioritize nearest deadline and highest module weighting.",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
