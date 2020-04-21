<template>
  <div>
    <div class="container">
      <div v-if="loaded===true" class="box">
        <service :data="posts" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import service from "../components/Service_Box.vue";
export default {
  components: {
    service
  },

  data() {
    return {
      posts: null,
      advance: false,
      loaded: false,
      id: this.$route.params.id
    };
  },
  methods: {
    ToggleValue() {
      this.advance = !this.advance;
    },
    refresh() {
      axios
        .get(`http://localhost:5151/app/request/` + this.id)
        .then(response => {
          this.posts = response.data.data;
          this.loaded = true;
        });
    }
  },
  mounted() {
    axios.get(`http://localhost:5151/app/request/` + this.id).then(response => {
      this.posts = response.data.data;
      this.loaded = true;
    });
  },
  watch: {
    $route: function() {
      this.id = this.$route.params.id;
      this.loaded = false;
      this.refresh();
    }
  }
};
</script>