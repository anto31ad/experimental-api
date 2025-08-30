<template>
  <div v-if="curService">
    <h1>{{ curService.name }}</h1>
    <p> {{ curService.description }}</p>
    <hr/>
    <ServiceInputForm/>
    <div v-if="responseData">
      <hr/>
      <h3>Response:</h3>
      <p class="json-block">
        {{ responseData }}
      </p>
    </div>
    <div v-if="serviceStore.hasErrors">
      <hr/>
      <div v-for="item in serviceStore.errorMessageList" :key="item">
          {{ item }}
      </div>
    </div>
  </div>
  <div v-else>
    Loading...
  </div>
</template>
<script setup lang="ts">
import { computed, watchEffect } from 'vue';
import { useRoute } from 'vue-router';

import { useServiceStore } from '@/stores/serviceStore';
import ServiceInputForm from './ServiceInputForm.vue';

const route = useRoute()
const serviceStore = useServiceStore()

const curService = computed(() => {
  return serviceStore.selectedService
})

const responseData = computed(() => {
  if (!curService.value?.lastResponse)
    return null

  let dataStr = '{}'
  try {
    dataStr = JSON.stringify(curService.value.lastResponse, null, 2)
  } catch {
    return null
  }
  console.log(dataStr)
  return dataStr
})

watchEffect(async () => {
  let serviceId = route.params.id
  if (Array.isArray(serviceId)) {
    serviceId = serviceId[0]
  }
  serviceStore.selectService(serviceId)
})
</script>

<style scoped>
.json-block {
  /* Ensure the font is monospaced for correct alignment */
  font-family: 'Inter', monospace;
  position: relative;
  min-height: 200px; /* Minimum height for better appearance */
  white-space: pre-wrap; /* whitespace-pre-wrap */
  word-break: break-all; /* break-words */
  text-align: left;
  background-color: #1a1a1a;
}
</style>