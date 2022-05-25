const proteinEnpoint = "http://127.0.0.1:5000/proteins/?";
const producerEnpoint = "http://127.0.0.1:5000/producers/";

const getProteins = async (
  producer,
  name,
  date_added,
  sortColumn,
  sortDirection,
  page,
  limit
) => {
  let url = proteinEnpoint;
  url += `page=${page}`;
  if (limit) url += `&limit=${limit}`;
  if (producer) url += `&producer=${producer}`;
  if (date_added) url += `&date_added=${date_added}`;
  if (name) url += `&name=${name}`;
  if (sortColumn) url += `&sort=${sortColumn}.${sortDirection}`;

  const response = await fetch(url);
  return response.json();
};

const getProducers = async () => {
  const response = await fetch(producerEnpoint);
  return response.json();
};

const proteinServie = { getProteins, getProducers };

export default proteinServie;
