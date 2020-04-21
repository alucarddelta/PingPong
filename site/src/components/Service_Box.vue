<template>
  <div>
    <nav class="level">
      <div>
        <p>
          <strong class="is-size-3">{{data.name}}</strong>
        </p>
        <p class="is-size-4">{{data.address}}</p>
      </div>
      <div class="navbar-end">
        <div class="navbar-item">
          <b-tag type="is-info" size="is-large">{{data.check_type}}</b-tag>
        </div>
        <div class="navbar-item">
          <div v-if="data.enabled == true">
            <b-tag type="is-success" size="is-large">Enabled</b-tag>
          </div>
          <div v-if="data.enabled == false">
            <b-tag type="is-danger" size="is-large">Disabled</b-tag>
          </div>
        </div>
        <div class="navbar-item">
          <div v-if="data.online == true">
            <b-tag type="is-success" size="is-large">Online</b-tag>
          </div>
          <div v-if="data.online == false">
            <b-tag type="is-danger" size="is-large">Offline</b-tag>
          </div>
        </div>
      </div>
    </nav>
    <div>
      <nav class="level">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Lowest Response (1 hr)</p>
            <p class="title">{{data.hour_low}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Highest Response (1 hr)</p>
            <p class="title">{{data.hour_high}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Successful Responses (1 hr)</p>
            <p class="title has-text-success">{{data.hour_successful}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Failed Responses (1 hr)</p>
            <p class="title has-text-danger">{{data.hour_fail}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Uptime (1 hr)</p>
            <p class="title">{{data.hour_successful/(data.hour_successful + data.hour_fail) * 100}}%</p>
          </div>
        </div>
      </nav>
      <nav class="level">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Lowest Response (24 hrs)</p>
            <p class="title">{{data.day_low}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Highest Response (24 hrs)</p>
            <p class="title">{{data.day_high}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Successful Responses (24 hrs)</p>
            <p class="title has-text-success">{{data.day_successful}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Failed Responses (24 hrs)</p>
            <p class="title has-text-danger">{{data.day_fail}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Uptime (24 hrs)</p>
            <p class="title">{{data.day_successful/(data.day_successful + data.day_fail) * 100}}%</p>
          </div>
        </div>
      </nav>
      <nav class="level">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Lowest Response (7 Days)</p>
            <p class="title">{{data.week_low}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Highest Response (7 Days)</p>
            <p class="title">{{data.week_high}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Successful Responses (7 Days)</p>
            <p class="title has-text-success">{{data.week_successful}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Failed Responses (7 Days)</p>
            <p class="title has-text-danger">{{data.week_fail}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Uptime (7 Days)</p>
            <p class="title">{{data.week_successful/(data.week_successful + data.week_fail) * 100}}%</p>
          </div>
        </div>
      </nav>
      <nav class="level">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Lowest Response (All time)</p>
            <p class="title">{{data.week_low}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Highest Response (All time)</p>
            <p class="title">{{data.week_high}} ms</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Successful Responses (All time)</p>
            <p class="title has-text-success">{{data.week_successful}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Failed Responses (All time)</p>
            <p class="title has-text-danger">{{data.week_fail}}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Uptime (All time)</p>
            <p class="title">{{data.week_successful/(data.week_successful + data.week_fail) * 100}}%</p>
          </div>
        </div>
      </nav>
    </div>
    <div v-if="data!==null">
      <chart :data="data" />
    </div>
  </div>
</template>

<script>
import chart from "./Service_Chart.vue";
export default {
  props: ["data"],
  components: { chart },
  data() {
    return {};
  }
};
</script>