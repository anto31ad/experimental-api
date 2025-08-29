<template>
  <h1>Experimental API</h1>
  <div v-if="serviceStore.services.length > 0">
    <ServicePicker :itemList="serviceStore.services"/>
  </div>
  <div v-else>
    Empty.
  </div>
</template>

<script setup lang="ts">
import { watchEffect } from 'vue'
import ServicePicker from '../components/ServicePicker.vue';
import { useServiceStore } from '../stores/serviceStore';

const serviceStore = useServiceStore();

watchEffect(() => {
  serviceStore.fetchServices()
});
</script>

<style scoped>
.app {
  max-width: 600px;
  margin: 2rem auto;
  font-family: sans-serif;
}
button {
  padding: 0.5rem 1rem;
}
</style>
