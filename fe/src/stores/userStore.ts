import { defineStore } from 'pinia'
import { DEV_OPTIONS } from '../constants'
import { requests } from '@/utils/requests'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    userGitHubId: '',
  }),
  actions: {
    clearState() {
      this.username = ''
      this.userGitHubId = ''
    },
    async fetchUserData() {
      if (DEV_OPTIONS.stubModeOn) {
        this.username = 'guest'
        return;
      }
      const user = await requests.requestThisUser()
      this.username = user.username
      this.userGitHubId = user.github_id
    },
  },
})
