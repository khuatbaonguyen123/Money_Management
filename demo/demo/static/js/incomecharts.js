const getIncomeData = () => {
    console.log("fetching");
    fetch("income_source_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const source_data = results.income_source_data;
        const [labels, data] = [
          Object.keys(source_data),
          Object.values(source_data),
        ];
  
        renderChart(data, labels);
      });
  };
  
  document.onload = getIncomeData();