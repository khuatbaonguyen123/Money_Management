const chartTypes = ['pie', 'bar', 'line', 'radar', 'doughnut'];
let currentChartTypeIndex = 0;

const getIncomeData = (selectedMonth, chartType) => {
  fetch(`income_source_summary/?selected_month=${selectedMonth}`)
    .then((res) => res.json())
    .then((results) => {
      console.log("results", results);
      const source_data = results.income_source_data;
      const [labels, data] = [
        Object.keys(source_data),
        Object.values(source_data),
      ];

      renderChart(data, labels, chartType);
    });
};
  
  document.addEventListener('DOMContentLoaded', function () {
    const monthSelect = document.getElementById('yourMonthSelect');
    const changeButton = document.getElementById('yourChangeButton');

    // Attach the event listener to the dropdown change event
    monthSelect.addEventListener('change', function () {
        const selectedMonth = monthSelect.value;
        if (selectedMonth) {
            const chartType = chartTypes[currentChartTypeIndex];
            getIncomeData(selectedMonth,chartType);
        }
    });

    // Attach the event listener to the "Change" button
    changeButton.addEventListener('click', function () {
      const selectedMonth = monthSelect.value;

      // Increment the chart type index
      currentChartTypeIndex = (currentChartTypeIndex + 1) % chartTypes.length;
      const chartType = chartTypes[currentChartTypeIndex];
      if (selectedMonth) {
          getIncomeData(selectedMonth, chartType);
      }
  });

  const initialSelectedMonth = monthSelect.value;
  const chartType = chartTypes[currentChartTypeIndex];
  getIncomeData(initialSelectedMonth,chartType);
});