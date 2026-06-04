import {
  LineChart,        // Tambahkan ini
  Line,             // Tambahkan ini
  CartesianGrid,    // Tambahkan ini
  XAxis,            // Tambahkan ini
  YAxis,            // Tambahkan ini
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#00ffff",
  "#ff00ff",
  "#00ff00",
  "#ff9900",
  "#ff0000",
  "#ffffff",
];

export default function ChartCard({
  title,
  data,
  selected,
}) {
  return (
    <div className="bg-slate-800 rounded-2xl p-5 shadow-lg border border-slate-700">
      <h2 className="text-xl font-bold mb-5 text-cyan-400">
        {title}
      </h2>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />

          <XAxis
            dataKey="created_at"
            stroke="#cbd5e1"
            tick={{ fontSize: 12 }}
          />

          <YAxis stroke="#cbd5e1" />

          <Tooltip />
          <Legend />

          {selected.map((item, index) => (
            <Line
              key={item}
              type="monotone"
              dataKey={item}
              stroke={COLORS[index % COLORS.length]}
              dot={false}
              strokeWidth={2}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}