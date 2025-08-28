<template>
  <div v-if="curService">
    <h1>{{ curService.name }}</h1>
    <p> {{ curService.description }}</p>
    <hr>
    <ServiceInputForm/>
  </div>
  <div v-else>
    Loading...
  </div>
</template>
<script setup lang="ts">
import { watchEffect } from 'vue';
import { useRoute } from 'vue-router';

import { useServiceStore } from '@/stores/serviceStore';
import { storeToRefs } from 'pinia';
import ServiceInputForm from './ServiceInputForm.vue';

const route = useRoute()
const serviceStore = useServiceStore()

//const serviceId = ref(null)
const { selectedService: curService } = storeToRefs(serviceStore)

watchEffect(async () => {
  let serviceId = route.params.id
  if (Array.isArray(serviceId)) {
    serviceId = serviceId[0]
  }
  serviceStore.fetchServiceById(serviceId)
})

</script>