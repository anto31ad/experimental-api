import { defineStore } from 'pinia'
import { requests } from '../utils/requests'

export interface ServiceParameter {
  name: string,
  expects: string,
}

export interface Service {
  id: string,
  name?: string,
  description?: string,
  thumbnail_url?: string,
  parameters?: ServiceParameter[],
  lastResponse?: JSON,
}

export const useServiceStore = defineStore('service', {
  state: () => ({
    services: [] as Service[],
    selectedServiceId: '' as string,
    loading: false,
    errorMessageList: [] as Array<string>,
  }),
  getters: {
    getList: (state) => state.services,
    isListEmpty: (state) => state.services.length < 1,
    selectedService: (state) => {
      return state.services.find(
        service => (service.id === state.selectedServiceId)
      )
    },
    hasErrors: (state) => state.errorMessageList.length > 0,
  },
  actions: {
    resetState() {
      this.loading = false
      this.errorMessageList = []
      this.services = []
      console.log("reset service state")
    },
    resetServiceRequestState() {
      this.loading = true
      this.errorMessageList = []
      console.log("reset service request state")
    },
    
    async fetchServices () {
      //skip if list is not empty
      if (!this.isListEmpty) {
        console.info("service list not empty")
        return;
      }
      console.info("fetching services...")
      this.resetState()
      try {
        this.services = await requests.requestListOfServices()
      } catch (err) {
        this.errorMessageList.push('Failed to fetch services: ' + err)
      } finally {
        this.loading = false
        this.fetchThumbnails()
      }
    },
    async fetchThumbnails() {
      if (this.isListEmpty) return;
      
      this.services.forEach(async (service) => {

        let thumb_url: string | null = null
        
        if (service.thumbnail_url) {
          thumb_url = await requests.getThumbnail(service.thumbnail_url)
          if (thumb_url) {
            service.thumbnail_url = thumb_url
            return;
          }
        }
        //fallback to random pic
        thumb_url = await requests.requestRandomPictureUrl()
        console.log(thumb_url)
        if (thumb_url) {
          service.thumbnail_url = thumb_url
          return;
        }
        service.thumbnail_url = undefined
      })
    },
    async fetchServiceById (serviceId: string) {

      this.resetServiceRequestState()
      this.selectedServiceId = serviceId
      console.log(`fetching service ${serviceId}`)
      try {
        const serviceInfo = await requests.requestServiceInfoById(serviceId)
        
        const index = this.services.findIndex(service => service.id === serviceId)
        if (index !== -1) {
          // Replace existing service with updated info
          this.services[index] = {
            ...this.services[index],
            ...serviceInfo
          }
        } else {
          // Add new service if not found
          console.log("Adding new service")
          this.services.push(serviceInfo)
        }
      } catch (err) {
        this.errorMessageList.push(`${err}`)
      } finally {
        this.loading = false
      }
    },
    async makeServiceRequest(
      serviceId: string,
      payload: JSON,
    ) {

      this.resetServiceRequestState()
      try {
        const responseData = await requests.requestOperationByServiceId(serviceId, payload)
        this.services.forEach(service => {
          if (service.id !== serviceId) return
          service.lastResponse = responseData
        })
      } catch (err) {
        this.errorMessageList.push(`Problem while making request to service '${serviceId}' :${err}`)
      } finally {
        this.loading = false
      }
    },
  },
})
