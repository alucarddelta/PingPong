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
            <div class="column">
              <b-field label="Port" label-position="labelPosition">
                <b-input v-model="data1.port" type="number"></b-input>
              </b-field>
            </div>
            <div class="column">
              <b-field label="Check Method">
                <b-select v-model="data1.check_method">
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
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
          <div class="columns">
            <div class="column">
              <b-field label="Timeout">
                <b-numberinput
                  v-model="data1.timeout"
                  min="5"
                  max="30"
                  controls-position="compact"
                  type="is-info"
                ></b-numberinput>
              </b-field>
            </div>
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
          <div class="buttons">
            <b-button icon-left="edit" type="is-info" v-on:click="update_data()">Update</b-button>
            <b-button icon-left="trash" type="is-danger" v-on:click="delete_data()">Delete</b-button>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
import { ToastProgrammatic as Toast } from "buefy";
import axios from "axios";
export default {
  props: ["data"],
  components: {},
  data() {
    return {
      data1: this.data
    };
  },
  methods: {
    update_data() {
      axios
        .put(`http://localhost:5151/app/request`, this.data1)
        .then(
          Toast.open({ message: "Editing " + this.data1.name, type: "is-info" })
        )
        .catch(err => {
          Toast.open({ message: err.message, type: "is-danger" });
        });
      setTimeout(function() {location.reload();}, 2000);
    },
    delete_data() {
      axios
        .delete(`http://localhost:5151/app/request/` + this.data1.xid)
        .then(
          Toast.open({
            message: "Deleteing " + this.data1.name,
            type: "is-danger"
          })
        )
        .catch(err => {
          Toast.open({ message: err.message, type: "is-danger" });
        });
     setTimeout(function() {location.reload();}, 2000);
    }
  }
};
</script>