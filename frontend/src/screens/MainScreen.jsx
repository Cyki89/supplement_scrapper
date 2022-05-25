import React, { useState, useEffect } from "react";
import Input from "../components/Input";
import Select from "../components/Select";
import Table from "../components/Table";
import proteinService from "../services/proteinService";
import Paginations from "../components/Paginations";
import useDebounce from "../hooks/useDebounce";

const pageLimits = [10, 20, 30];

const MainScreen = () => {
  const [proteins, setProteins] = useState([]);
  const [producers, setProducers] = useState([]);
  const [producer, setProducer] = useState("");
  const [proteinName, setProteinName] = useState("");
  const [searchProteinName, setSearchProteinName] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [sortColumn, setSortColumn] = useState("");
  const [sortDirection, setSordDirection] = useState("");

  const [pageLimit, setPageLimit] = useState("");
  const [currPage, setCurrPage] = useState(1);
  const [lastPage, setLastPage] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      const producers = await proteinService.getProducers();
      setProducers(producers);
    };

    fetchData();
  }, []);

  const handleProducerChange = (e) => {
    setCurrPage(1);
    setProducer(e.target.value);
  };

  const handleChangeSearchProteinName = (e) => {
    setSearchProteinName(e.target.value);
  };

  const handleChangeProteinName = () => {
    setProteinName(searchProteinName);
    setCurrPage(1);
  };

  useDebounce(handleChangeProteinName, 1000, [searchProteinName]);

  const handleDateChange = (e) => {
    setCurrPage(1);
    setSelectedDate(e.target.value);
  };

  const handleSort = (colName) => {
    setCurrPage(1);

    if (colName === sortColumn) {
      setSordDirection(() => (sortDirection === "asc" ? "desc" : "asc"));
      return;
    }
    setSortColumn(colName);
    setSordDirection("asc");
  };

  const handlePageLimitChange = (e) => {
    setCurrPage(1);
    setPageLimit(e.target.value);
  };

  const handlePageChange = (page) => setCurrPage(page);

  useEffect(() => {
    const fetchData = async () => {
      const response = await proteinService.getProteins(
        producer,
        proteinName,
        selectedDate,
        sortColumn,
        sortDirection,
        currPage,
        pageLimit
      );
      const count = response["count"];
      const data = response["results"];

      setLastPage(Math.ceil(count / (pageLimit || pageLimits[0])));
      setProteins(data);
    };

    fetchData();
  }, [
    currPage,
    proteinName,
    producer,
    selectedDate,
    sortColumn,
    sortDirection,
    pageLimit,
  ]);

  const columns = [
    {
      label: "Producer",
      path: "producer",
    },
    {
      label: "Image",
      path: "image",
      content: (product) => (
        <img src={product.image} alt="No Data" width="75em" height="75em"></img>
      ),
    },
    {
      label: "Name",
      path: "name",
      content: (product) => (
        <a href={product.url} target="_blank" rel="noreferrer">
          {product.name}
        </a>
      ),
      sortable: true,
    },
    {
      label: "Date",
      path: "date_added",
    },
    {
      label: "Weight",
      path: "weight",
      sortable: true,
    },
    {
      label: "Price",
      path: "price",
      sortable: true,
    },
    {
      label: "Old_price",
      path: "old_price",
    },
    {
      label: "Discount",
      path: "discount",
      sortable: true,
    },

    {
      label: "Price_standarized",
      path: "price_standarized",
      sortable: true,
    },
  ];

  return (
    <>
      <div className="filter-container">
        <Select
          name="Producer"
          className="select"
          onChange={handleProducerChange}
          options={producers}
          value={producer}
        />
        <Input
          label="Date"
          value={selectedDate}
          onChange={handleDateChange}
          type="date"
        />

        <Input
          label="Search"
          value={searchProteinName}
          onChange={handleChangeSearchProteinName}
        />
      </div>

      <Table
        columns={columns}
        data={proteins}
        sortColumn={sortColumn}
        sortOrder={sortDirection}
        onSort={handleSort}></Table>

      <div className="bottom-container">
        <Paginations
          currentPage={currPage}
          lastPage={lastPage}
          onChange={handlePageChange}
        />
        {lastPage > 1 && (
          <Select
            name="Page Limit"
            className="select-limit"
            onChange={handlePageLimitChange}
            options={pageLimits}
            value={pageLimit}
          />
        )}
      </div>
    </>
  );
};

export default MainScreen;
