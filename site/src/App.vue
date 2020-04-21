<template>
  <div id="app">
    <div id="nav">
      <b-navbar type="is-primary">
        <template slot="brand">
          <b-navbar-item tag="router-link" :to="{ path: '/' }">
            <strong>PingPlotter</strong>
          </b-navbar-item>
        </template>
        <template slot="start" v-if="posts.core.heading !== null">
          <b-navbar-item tag="router-link" :to="{ path: '/' }">Home</b-navbar-item>
          <b-navbar-dropdown v-if="posts.menu.length !== 0" label="Services">
            <div v-for="x in posts.menu" v-bind:key="x.xid">
              <b-navbar-item tag="router-link" :to="'/service/' + x.xid">{{x.name}}</b-navbar-item>
            </div>
          </b-navbar-dropdown>
          <b-navbar-dropdown label="Config">
            <b-navbar-item tag="router-link" to="/config/services">Services</b-navbar-item>
            
            <b-navbar-item tag="router-link" to="/config/server">Server Settings</b-navbar-item>
          </b-navbar-dropdown>
          <b-navbar-item tag="router-link" to="/about">About</b-navbar-item>
        </template>
      </b-navbar>
    </div>
    <div class="container">
      <div v-if="loaded === true && posts.core.heading === null" class="box">
        <setup />
      </div>
      <div v-else class="box">
        <p class="title is-1 is-spaced has-text-centered">{{posts.core.heading}}</p>
        <p class="subtitle is-3 has-text-centered">{{posts.core.subheading}}</p>
      </div>
      <hr />
      <div v-if="posts.core.heading !== null">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import setup from "./components/Home_config";

export default {
  components: { setup },
  data() {
    return {
      loaded: false,
      posts: {
        menu: [],
        core: {
          heading: null,
          subheading: null
        }
      }
    };
  },
  mounted() {
    axios.get(`http://localhost:5151/home`).then(response => {
      this.posts = response.data.data;
      this.loaded = true;
    });
  }
};
</script>

<style lang="scss">
@import "~@fortawesome/fontawesome-free/scss/fontawesome.scss";
@import "~@fortawesome/fontawesome-free/css/all.css";
@import "styles.scss";

// padding to account for sidebar size
.hero-body {
  padding-top: 0px;
  padding-right: 0px;
  padding-left: 250px;
}
.hero-body.collapsed {
  padding-left: 50px;
}
.is-main-content {
  padding-left: 25px;
}
</style>

