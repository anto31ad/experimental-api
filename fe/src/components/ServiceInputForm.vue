<template>
  <form v-if="curService && formData" @submit.prevent="submitForm" class="form-grid">
    <div v-for="param in curService.parameters">
      <label :for="param.name">{{ param.name }} ({{ param.description }})</label>
      <input
        :id="param.name"
        v-model="formData[param.name]"
        :title="param.name"
        required />
    </div>
    <button type="submit" class="full-width">Submit</button>
  </form>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
import { useServiceStore } from '@/stores/serviceStore';

const serviceStore = useServiceStore()
const { selectedService: curService } = storeToRefs(serviceStore)

const formData = ref()

onMounted(()=> {
  if (curService.value?.parameters) {
    formData.value = Object.fromEntries(
      curService.value.parameters.map(param => [param.name, null])
    )
  }
})

function submitForm() {
  console.log('Form submitted:', formData.value)
  if (curService.value?.id){
    serviceStore.makeServiceRequest(curService.value?.id, formData.value)
  }
}
</script>

<style scoped>
.form-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr 1fr;
  max-width: 600px;
  margin: auto;
}

.form-grid > div {
  display: flex;
  flex-direction: column;
}

.full-width {
  grid-column: span 2;
  text-align: center;
}
</style>