<template>
  <div>
    <VueApexCharts height="200" type="area" :options="chartOptions" :series="series"></VueApexCharts>
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
          name: "Respose time",
          data: this.data
        }
      ],
      chartOptions: {
        colors:['#2a3f54'],
        chart: {
          type: "area",
          height: 350
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          type: "datetime",
          tickAmount: 6
        },
        yaxis: {
          title: {
            text: "milliseconds"
          }
        },
        tooltip: {
          x: {
            format: "dd MMM yyyy HH:mm:ss"
          }
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 1,
            opacityTo: 0.99,
            stops: [0, 100]
          }
        }
      }
    };
  }
};
</script>