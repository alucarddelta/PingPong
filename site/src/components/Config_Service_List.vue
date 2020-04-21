<template>
  <div>
    <h1 class="title">List</h1>
    <b-table
      :data="posts"
      ref="table"
      paginated
      per-page="5"
      detailed
      aria-next-label="Next page"
      aria-previous-label="Previous page"
      aria-page-label="Page"
      aria-current-label="Current page"
    >
      <template slot-scope="props">
        <b-table-column field="name" label="Name">{{ props.row.name }}</b-table-column>

        <b-table-column field="check_type" label="Type" width="150">{{ props.row.check_type }}</b-table-column>
        <b-table-column field="notifying" label="Notifying" width="150">
          <div v-if="props.row.allow_notifications === true">
            <b-icon icon="check-circle" type="is-success" />
          </div>
          <div v-else>
            <b-icon icon="times-circle" type="is-danger" />
          </div>
        </b-table-column>
        <b-table-column field="enabled" label="Enabled" width="150">
          <div v-if="props.row.enabled === true">
            <b-icon icon="check-circle" type="is-success" />
          </div>
          <div v-else>
            <b-icon icon="times-circle" type="is-danger" />
          </div>
        </b-table-column>
      </template>

      <template slot="detail" slot-scope="props">
        <div class="box">
          <div v-if="props.row.check_type==='ICMP'">
            <item_ICMP :data="props.row" v-on:refresh="refresh()" />
          </div>
          <div v-if="props.row.check_type==='TCP'">
            <item_TCP :data="props.row" v-on:refresh="refresh()" />
          </div>
        </div>
      </template>
    </b-table>
  </div>
</template>

<script>
import axios from "axios";
import item_ICMP from "../components/Config_Service_Item_ICMP.vue";
import item_TCP from "../components/Config_Service_Item_TCP.vue";
import { ToastProgrammatic as Toast } from "buefy";
export default {
  components: {
    item_ICMP,
    item_TCP
  },
  data() {
    return {
      posts: []
    };
  },
  mounted() {
    axios
      .get(`http://localhost:5151/app/config/service`)
      .then(response => {
        this.posts = response.data.data;
      })
      .catch(err => {
        Toast.open({ message: err.message, type: "is-danger" });
      });
  }
};
</script>