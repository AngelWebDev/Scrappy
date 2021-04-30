<template>
  <div class="counter">
        <button @click="decrement">-</button>
        <span>{{ count }}</span>
        <button @click="increment">+</button>
    </div>
</template>

<script>
export default {
  // let's create a Counter component
  name: 'Counter',
  computed: {
    count () {
      return this.$store.state.count
    }
  },
  methods: {
    increment () { this.$store.commit('increment') },
    decrement () { this.$store.commit('decrement') }
  }
}
</script>
