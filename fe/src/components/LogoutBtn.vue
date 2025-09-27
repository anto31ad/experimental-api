<template>
  <button @click="requests.logout">
    Log out
  </button>
</template>
  
<script setup lang="ts">
import { requests } from '@/utils/requests';
</script>
