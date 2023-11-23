const getIncomeData = () => {
    console.log("fetching");
    fetch("pie_chart")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results);
        const source_data = results.income_data;
        const [labels, data] = [
          Object.keys(source_data),
          Object.values(source_data),
        ];
  
        renderChart(data, labels);
      });
  };
  
  document.onload = getIncomeData();