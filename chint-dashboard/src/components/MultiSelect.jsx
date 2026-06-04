export default function MultiSelect({
  options,
  selected,
  setSelected,
}) {
  const handleToggle = (item) => {
    if (selected.includes(item)) {
      setSelected(selected.filter((i) => i !== item));
    } else {
      setSelected([...selected, item]);
    }
  };

  return (
    <div className="flex flex-wrap gap-3 mb-5">
      {options.map((item) => (
        <button
          key={item}
          onClick={() => handleToggle(item)}
          className={`px-4 py-2 rounded-xl border transition-all
          ${
            selected.includes(item)
              ? "bg-cyan-500 text-white border-cyan-500"
              : "bg-slate-800 border-slate-600 text-slate-300"
          }`}
        >
          {item.toUpperCase()}
        </button>
      ))}
    </div>
  );
}