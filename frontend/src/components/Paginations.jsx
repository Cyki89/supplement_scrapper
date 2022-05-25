import React from "react";

const Paginations = ({ currentPage, lastPage, onChange }) => {
  if (lastPage <= 1) return null;
  return (
    <div className="pagination-container">
      {currentPage !== 1 && (
        <button className="btn-pagination" onClick={() => onChange(1)}>
          &lt;&lt;&lt;
        </button>
      )}
      {currentPage !== 1 && (
        <button className="btn-pagination" onClick={() => onChange(1)}>
          {1}
        </button>
      )}
      {currentPage - 3 > 1 && <span className="elipsis">&#8230;</span>}
      {currentPage - 2 > 1 && (
        <button
          className="btn-pagination"
          onClick={() => onChange(currentPage - 2)}>
          {currentPage - 2}
        </button>
      )}
      {currentPage - 1 > 1 && (
        <button
          className="btn-pagination"
          onClick={() => onChange(currentPage - 1)}>
          {currentPage - 1}
        </button>
      )}
      <button className="btn-pagination active">{currentPage}</button>
      {currentPage + 1 < lastPage && (
        <button
          className="btn-pagination"
          onClick={() => onChange(currentPage + 1)}>
          {currentPage + 1}
        </button>
      )}
      {currentPage + 2 < lastPage && (
        <button
          className="btn-pagination"
          onClick={() => onChange(currentPage + 2)}>
          {currentPage + 2}
        </button>
      )}
      {currentPage + 3 < lastPage && <span className="elipsis">&#8230;</span>}
      {currentPage !== lastPage && (
        <button className="btn-pagination" onClick={() => onChange(lastPage)}>
          {lastPage}
        </button>
      )}
      {currentPage !== lastPage && (
        <button className="btn-pagination" onClick={() => onChange(lastPage)}>
          &gt;&gt;&gt;
        </button>
      )}
    </div>
  );
};

export default Paginations;
