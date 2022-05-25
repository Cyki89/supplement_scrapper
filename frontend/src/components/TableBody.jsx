import React from "react";

const TableBody = ({ columns, data }) => {
  const renderCell = (item, column) => {
    if (column.content) return column.content(item);

    const pathItems = column.path.split(".");

    let newItem = { ...item };
    for (let i = 0; i < pathItems.length; ++i) {
      newItem = newItem[pathItems[i]];
    }

    return newItem;
  };

  const createTdKey = (idx, column) => `${idx}${column.path}`;

  return (
    <tbody>
      {data.map((item, idx) => (
        <tr key={idx}>
          {columns.map((column) => (
            <td key={createTdKey(idx, column)}>{renderCell(item, column)}</td>
          ))}
        </tr>
      ))}
    </tbody>
  );
};

export default TableBody;
