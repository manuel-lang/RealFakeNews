function triggerProcessing(text, summarize) {
  let data = {};
  data["text"] = text;
  data["summarize"] = summarize;
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
  return fetch("http://localhost:8000", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
      return null;
    });
}

export default triggerProcessing;
