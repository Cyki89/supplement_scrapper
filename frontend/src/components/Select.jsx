import React from "react";

const Select = ({ name, className, onChange, options, value }) => {
  return (
    <select className={className} onChange={onChange} value={value}>
      <option value="">Select {name}</option>
      {options.map((option, idx) => (
        <option key={idx} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
};

export default Select;
