<template>
  <div class="card">
    <img
      :src="thumbnail_url"
      alt="Card image"
      class="card-image" />
    <div class="card-body">
      <h2 class="card-title">
        <div v-if="title" class="truncate">{{ title }}</div>
        <div v-else>Untitled</div>
      </h2>
      <p class="card-text truncate">
        <span v-if="text">{{ text }}</span>
        <span v-else>No description available.</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useServiceStore } from '@/stores/serviceStore';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const serviceStore = useServiceStore()
const { thumbnails } = storeToRefs(serviceStore) 

const props = defineProps({
  title: String,
  text: String,
  serviceId: String,
})

const thumbnail_url = computed(() => {
  if (props.serviceId) {
    return thumbnails.value[props.serviceId]
  }
  return 'loading.png'
})

</script>
<style scoped>
.card {
  min-width: 200px;
  min-height: 300px;
  max-width: 400px;
  max-height: 400px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background-color: #2c3657;
  display: flex;
  flex-direction: column;
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.card-title {
  font-size: 1.2rem;
  margin: 10px 10px 10px 10px;
  color: #ffffff;
  overflow: hidden;
}

h2 {
  margin: 0px;
}

.card-text {
  color: #a7a7a7;
  font-size: 0.95rem;
  margin: 0px 10px 20px 10px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.truncate {
  display: -webkit-box; /* Enables multi-line truncation */
  -webkit-line-clamp: 3; /* Limits the text to 3 lines */
  line-clamp: 3; /* Standard property for compatibility */
  -webkit-box-orient: vertical; /* Required for -webkit-line-clamp to work */
  max-height: calc(1.2em * 3); /* Adjust based on font size and line count */
}
</style>