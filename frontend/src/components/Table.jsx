import React from "react";
import TableHeaders from "./TableHeaders";
import TableBody from "./TableBody";

const Table = ({ columns, data, sortColumn, sortOrder, onSort }) => {
  return (
    <table>
      <TableHeaders
        columns={columns}
        sortColumn={sortColumn}
        sortOrder={sortOrder}
        onSort={onSort}
      />
      <TableBody columns={columns} data={data} />
    </table>
  );
};

export default Table;
