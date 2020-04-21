<template>
  <div>
    <div class="columns">
      <div class="column">
        <b-field label="Heading">
          <b-input v-model="heading" placeholder="Ping Plotter"></b-input>
        </b-field>
      </div>
      <div class="column">
        <b-field label="Sub Heading">
          <b-input v-model="sub" placeholder="Pings 'r' Us"></b-input>
        </b-field>
      </div>
    </div>
    <b-button v-on:click="update_data()" type='is-info'>Submit</b-button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  components: {},
  data() {
    return {
      heading: null,
      sub: null,
      response: null
    }
  },
  methods: {
    update_data() {
      axios
        .post(`http://localhost:5151/app/home`, {
          heading: this.heading,
          subheading: this.sub
        })
        .then(response => {
          this.response = response.data.data;
        }).catch(err =>{console.log(err)} );setTimeout(function() {location.reload();}, 2000);
    }
  }
};
</script>

<style>
</style>