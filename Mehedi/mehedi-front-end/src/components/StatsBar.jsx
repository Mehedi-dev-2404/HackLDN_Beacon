// StatsBar - Quick stats badges from Mohammed code.html
// Shows: universities, jobs, funding at a glance

export default function StatsBar({ stats }) {
  const defaultStats = {
    unis: 169,
    jobs: 768,
    funding: '£3.4k'
  };

  const data = stats || defaultStats;

  return (
    <div className="flex flex-wrap gap-3 animate-fade-in">
      <div className="flex items-center gap-2 px-3 py-1.5 border border-gray-800 text-xs">
        <span className="text-gray-500">◆</span>
        <span className="tracking-wider">{data.unis} unis</span>
      </div>
      <div className="flex items-center gap-2 px-3 py-1.5 border border-gray-800 text-xs hover:border-gray-600 transition-colors cursor-pointer">
        <span className="text-gray-500">▪</span>
        <span className="tracking-wider">{data.jobs} jobs</span>
      </div>
      <div className="flex items-center gap-2 px-3 py-1.5 border border-gray-800 text-xs hover:border-gray-600 transition-colors cursor-pointer">
        <span className="text-gray-500">$</span>
        <span className="tracking-wider">{data.funding} funding</span>
      </div>
    </div>
  );
}
