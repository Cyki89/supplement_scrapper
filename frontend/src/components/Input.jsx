import React from "react";

const Input = ({ label, onChange, value, type = "Text" }) => {
  return (
    <div>
      <input
        placeholder={label}
        onChange={onChange}
        className="input"
        value={value}
        type={type}
      />
    </div>
  );
};

export default Input;
