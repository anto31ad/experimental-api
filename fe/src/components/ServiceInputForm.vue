<template>
  <form v-if="curService && formData" @submit.prevent="submitForm" class="form-grid">
    <div v-for="param in props.curService.parameters">
      <label :for="param.name">{{ param.name }}</label>
      <textarea
        :id="param.name"
        v-model="formData[param.name]"
        :title="param.description"
        required></textarea>
    </div>
    <button type="submit" class="full-width">Submit</button>
  </form>
</template>

<script setup lang="ts">
import type { Service } from '@/stores/serviceStore';
import { onMounted, ref } from 'vue';
import { useServiceStore } from '@/stores/serviceStore';

const serviceStore = useServiceStore()

const formData = ref()

const props = defineProps<{
  curService: Service
}>()

onMounted(()=> {
  if (props.curService?.parameters) {
    formData.value = Object.fromEntries(
      props.curService.parameters.map(param => [param.name, null])
    )
  }
})

function submitForm() {
  if (props.curService?.id){
    serviceStore.makeServiceRequest(
      props.curService?.id, JSON.parse(JSON.stringify(formData.value))
    )
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