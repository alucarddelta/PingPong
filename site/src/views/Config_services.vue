<template>
  <div>
    <section>
      <div class="container">
        <div class="box"><create /></div>
      </div>
    </section>
    <hr />
    <section>
      <div class="container">
        <div class="box">
          <list />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import list from "../components/Config_Service_List.vue";
import create from "../components/Config_Service_Create.vue";
export default {
  components: {
    list, create
  }
};
</script>

<style>
</style>