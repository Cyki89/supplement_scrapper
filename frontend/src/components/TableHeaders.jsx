import React from "react";

const TableHeaders = ({ columns, sortColumn, sortOrder, onSort }) => {
  const renderSortIcon = (column) => {
    if (!column.sortable) return;

    let sortIconClass = "fa fa-sort clickable";
    if (!sortColumn || column.path !== sortColumn)
      return <i className={sortIconClass}></i>;

    console.log(sortOrder);
    sortIconClass =
      sortOrder === "asc"
        ? "fa fa-sort-desc clickable"
        : "fa fa-sort-asc clickable";

    return <i className={sortIconClass}></i>;
  };

  return (
    <thead>
      <tr>
        {columns.map((column) => (
          <th
            key={column.label}
            onClick={column.sortable ? (e) => onSort(column.path) : null}>
            {column.label} {renderSortIcon(column)}
          </th>
        ))}
      </tr>
    </thead>
  );
};

export default TableHeaders;
