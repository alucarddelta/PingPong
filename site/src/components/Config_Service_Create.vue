<template>
  <div>
    <h1 class="title">Create</h1>
    <b-field label="Service Type" label-position="labelPosition">
      <b-field>
        <b-select v-model="check_type">
          <option value="ICMP">ICMP</option>
          <option value="TCP">TCP</option>
        </b-select>
      </b-field>
    </b-field>
    <div v-if="check_type === 'ICMP'">
      <ICMP_select/>
    </div>
    <div v-if="check_type === 'TCP'">
      <TCP_select/>
    </div>
  </div>
</template>

<script>
import ICMP_select from "./Config_Service_Create_ICMP"
import TCP_select from "./Config_Service_Create_TCP"
export default {
  props: ["data"],
  components: {ICMP_select, TCP_select},
  data() {
    return {
      check_type: 'ICMP',
    };
  }
};
</script>