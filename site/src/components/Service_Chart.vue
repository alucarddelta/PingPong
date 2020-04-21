<template>
  <div>
    <div id="wrapper">
      <div id="chart-line2">
        <VueApexCharts type="line" height="230" :options="chartOptions" :series="series"></VueApexCharts>
      </div>
      <div id="chart-line">
        <VueApexCharts type="area" height="130" :options="chartOptionsLine" :series="seriesLine"></VueApexCharts>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
export default {
  props: ["data"],
  components: {
    VueApexCharts
  },

  data() {
    return {
      series: [
        {
          data: this.data.chartformat
        }
      ],
      chartOptions: {
        chart: {
          id: "chart2",
          type: "line",
          height: 230,
          toolbar: {
            autoSelected: "pan",
            show: false
          }
        },
        colors: ["#2a3f54"],
        stroke: {
          width: 3
        },
        dataLabels: {
          enabled: false
        },
        fill: {
          opacity: 1
        },
        markers: {
          size: 0
        },
        xaxis: {
          type: "datetime"
        }
      },

      seriesLine: [
        {
          data: this.data.chartformat
        }
      ],
      chartOptionsLine: {
        chart: {
          id: "chart1",
          height: 130,
          type: "area",
          brush: {
            target: "chart2",
            enabled: true
          },
          selection: {
            enabled: true,
            xaxis: {
              min: this.data.time_day,
              max: this.data.time_now
            }
          }
        },
        colors: ["#2a3f54"],
        fill: {
          type: "gradient",
          gradient: {
            opacityFrom: 0.91,
            opacityTo: 0.1
          }
        },
        xaxis: {
          type: "datetime",
          tooltip: {
            enabled: false
          }
        },
        yaxis: {
          tickAmount: 2
        }
      }
    };
  }
};
</script>