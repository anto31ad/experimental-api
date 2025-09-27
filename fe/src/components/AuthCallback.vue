<template>
  <div>Authenticating...</div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (!token) {
      console.error("No token found");
      return;
    }
    localStorage.setItem('jwt_token', token);

    await userStore.fetchUserData()
    router.replace({ path: '/' })
  } catch (e) {
    console.error(e)
    router.replace({ path: '/login' })
  }
})
</script>