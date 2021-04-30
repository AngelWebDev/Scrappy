<template>
  <v-navigation-drawer absolute width="260px" permanent>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">
          Scrappy
        </v-list-item-title>
        <v-list-item-subtitle> </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list nav dense>
      <v-list-item-group v-model="selectedItem" color="primary">
        <v-list-item
          v-for="({ icon, title, target }, i) in items"
          :key="i"
          :href="target"
          link
        >
          <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title
              v-text="$t(`side-bar.${title}`)"
            ></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'navigation-bar',
  components: {},
  props: {
    selectedItem: Number
  },
  data () {
    return {
      items: [
        { title: 'arrival', icon: 'mdi-dolly', target: '/arrival' },
        { title: 'payout', icon: 'mdi-credit-card-outline', target: '/payout' },
        { title: 'office', icon: 'mdi-office-building', target: '/office' }
      ],
      right: null,
      user: {}
    }
  },
  created () {
    // eslint-disable-next-line no-undef
    this.user = authUser
    this.items = this.items.filter((item) => this.user[item.title])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.v-navigation-drawer {
  -webkit-box-shadow: 0 2px 4px -1px rgb(0 0 0 / 20%),
    0 4px 5px 0 rgb(0 0 0 / 14%), 0 1px 10px 0 rgb(0 0 0 / 12%);
  box-shadow: 0 2px 4px -1px rgb(0 0 0 / 20%), 0 4px 5px 0 rgb(0 0 0 / 14%),
    0 1px 10px 0 rgb(0 0 0 / 12%);
  z-index: 2;
}
.v-list-item__title.title {
  margin-top: 10px;
}
</style>
