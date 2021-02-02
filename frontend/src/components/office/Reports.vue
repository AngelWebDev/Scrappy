<template>
  <div class="users">
    Reports
  </div>
</template>

<script>
export default {
  name: "reports",
  components: {},
  data() {
    return {
      items: [
        { title: "Arrival", icon: "mdi-dolly" },
        { title: "Payout", icon: "mdi-credit-card-outline" },
        { title: "Office", icon: "mdi-office-building" },
      ],
      right: null,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.users {
  margin-left: 260px;
}
</style>
