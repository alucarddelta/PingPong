<template>
  <div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child">
          <div class="columns">
            <div class="column">
              <b-field label="Name" label-position="labelPosition">
                <b-input v-model="data1.name"></b-input>
              </b-field>
            </div>
            <div class="column">
              <b-field label="Address" label-position="labelPosition">
                <b-input v-model="data1.address"></b-input>
              </b-field>
            </div>
          </div>
        </article>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child">
          <div class="columns">
            <div class="column">
              <b-field label="Notifications">
                <b-select v-model="data1.allow_notifications">
                  <option value="true">Enable</option>
                  <option value="false">Disabled</option>
                </b-select>
              </b-field>
            </div>
            <div class="column">
              <b-field label="All Notifications">
                <b-select v-model="data1.all_notifications">
                  <option value="true">Enable</option>
                  <option value="false">Disabled</option>
                </b-select>
              </b-field>
            </div>
            <div class="column">
              <b-field label="Home Screen">
                <b-select v-model="data1.visible">
                  <option value="true">Enable</option>
                  <option value="false">Disabled</option>
                </b-select>
              </b-field>
            </div>
            <div class="column">
              <b-field label="Enabled">
                <b-select v-model="data1.enabled">
                  <option value="true">Enable</option>
                  <option value="false">Disabled</option>
                </b-select>
              </b-field>
            </div>
          </div>
        </article>
      </div>
    </div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child">
          <b-button icon-left="plus" type="is-info" v-on:click="update_data()">Create</b-button>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ToastProgrammatic as Toast } from 'buefy'
export default {
  components: {},
  data() {
    return {
      posts: null,
      data1: {name: null,
      address: null,
      visible: true,
      allow_notifications: false,
      all_notifications: false,
      enabled: true,
      check_type: 'ICMP'}
    };
  },
  methods: {
    update_data() {
      axios
        .post(`http://localhost:5151/app/request`, this.data1)
        .then(Toast.open({ message: 'Adding ' + this.data1.name, type: "is-info" }))
        .catch(err => {
          Toast.open({ message: err.message, type: "is-danger" });
        });
      setTimeout(function() { location.reload(); }, 1000);
    }
  }
};
</script>
