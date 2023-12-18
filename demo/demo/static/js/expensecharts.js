const chartTypes = ['pie', 'bar', 'line', 'radar', 'doughnut', 'bubble'];
let currentChartTypeIndex = 0;

const getCategoryData = (selectedMonth, chartType) => {
  fetch(`expense_category_summary/?selected_month=${selectedMonth}`)
    .then((res) => res.json())
    .then((res1) => {
      console.log("result", res1);
      const results = res1.expense_category_data;
      const [labels, data] = [
        Object.keys(results),
        Object.values(results)
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
        getCategoryData(selectedMonth,chartType);
      }
  });

  // Attach the event listener to the "Change" button
  changeButton.addEventListener('click', function () {
    const selectedMonth = monthSelect.value;

    // Increment the chart type index
    currentChartTypeIndex = (currentChartTypeIndex + 1) % chartTypes.length;
    const chartType = chartTypes[currentChartTypeIndex];
    if (selectedMonth) {
      getCategoryData(selectedMonth, chartType);
    }
  });

  const initialSelectedMonth = monthSelect.value;
  const chartType = chartTypes[currentChartTypeIndex];
  getCategoryData(initialSelectedMonth,chartType);
});