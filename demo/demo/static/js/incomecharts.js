const getIncomeData = (selectedMonth) => {
  console.log("fetching");
  fetch(`income_source_summary/?selected_month=${selectedMonth}`)
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
  
  document.addEventListener('DOMContentLoaded', function () {
    const monthSelect = document.getElementById('yourMonthSelect');

    // Attach the event listener to the dropdown change event
    monthSelect.addEventListener('change', function () {
        const selectedMonth = monthSelect.value;
        if (selectedMonth) {
            getIncomeData(selectedMonth);
        }
    });
});