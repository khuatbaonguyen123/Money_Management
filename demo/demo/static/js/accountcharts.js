const getAccountData = () => {
    console.log("fetching");
    fetch("account_amount")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const source_data = results.account_data;
        const [labels, data] = [
          Object.keys(source_data),
          Object.values(source_data),
        ];
  
        renderChart(data, labels, 'bar');
      });
  };
  
  document.onload = getAccountData();