<template>
  <div>
    <nav class="level">
      <strong class="is-size-3">{{data.name}}</strong>
      <div class="navbar-end">
        <div class="navbar-item">
          <b-button type="is-primary" @click="ToggleValue()">Stats</b-button>
        </div>
        <div v-if='data.no_data' class="navbar-item">
          <b-tag  type='is-success' size="is-large">No Recent Data</b-tag>
        </div>
        <div class="navbar-item">
          <b-tag type="is-info" size="is-large">{{data.check_type}}</b-tag>
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
    <div v-if="advance===false">
      <chart :data="data.chartformat" />
    </div>
    <div v-if="advance===true">
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
      <div class="buttons">
        <b-button
          type="is-primary"
          expanded
          tag="router-link"
          :to="'/service/' + data.xid"
        >Advance View</b-button>
      </div>
    </div>
  </div>
</template>

<script>
import chart from "./Home_Chart.vue";
export default {
  props: ["data"],
  components: {
    chart
  },

  data() {
    return {
      posts: [],
      errors: [],
      advance: false
    };
  },
  methods: {
    ToggleValue() {
      this.advance = !this.advance;
    }
  }
};
</script>