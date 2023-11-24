const getCategoryData = () => {
  fetch("expense_full_chart")
    .then((res) => res.json())
    .then((res1) => {
      console.log("result", res1);
      const results = res1.expense_data;
      const [labels, data] = [
        Object.keys(results),
        Object.values(results)
      ];

      renderChart(data, labels);
    });

};

document.onload = getCategoryData();
