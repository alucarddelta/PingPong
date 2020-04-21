<template>
  <div>
    <div v-if="posts === null || posts === []">
      <div class="box">
        <h1>Nothing To See Here</h1>
      </div>
    </div>
    <div v-for="x in posts" v-bind:key="x.xid">
      <div class="container">
        <div class="box">
          <box :data="x" />
        </div>
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import box from "../components/Home_Box.vue";
export default {
  components: {
    box
  },

  data() {
    return {
      posts: [],
      advance: false
    };
  },
  methods: {
    ToggleValue() {
      this.advance = !this.advance;
    }
  },
  mounted() {
    axios.get(`http://localhost:5151/app/request`).then(response => {
      this.posts = response.data.data;
    });
  }
};
</script>