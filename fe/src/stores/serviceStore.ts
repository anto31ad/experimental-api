import { defineStore } from 'pinia'
import { requests } from '../utils/requests'
import { API_ENDPOINTS } from '@/constants'

export interface ServiceOverview {
  id: string,
  name?: string,
  description?: string,
  thumbnail_url?: string,
}

export interface ServiceParameter {
  name: string,
  expects: string,
}

export interface Service {
  id: string,
  name?: string,
  description?: string,
  parameters?: ServiceParameter[],
}

export const useServiceStore = defineStore('service', {
  state: () => ({
    services: [] as ServiceOverview[],
    selectedService: null as Service | null,
    thumbnails: {} as { [key: string]: string },
    loading: false,
    errorMessageList: [] as Array<string>,
    lastResponse: null as JSON | null,
  }),
  getters: {
    getList: (state) => state.services,
    isListEmpty: (state) => state.services.length < 1,
    getSelected: (state) => state.selectedService,
    hasErrors: (state) => state.errorMessageList.length > 0,
  },
  actions: {
    clearState() {
      this.loading = false
      this.errorMessageList = []
      this.lastResponse = null
      this.services = []
      this.selectedService = null
      console.log("cleared service state")
    },
    initUtils() {
      this.loading = true
      this.errorMessageList = []
      console.log("initialized service utils")
    },
    
    async fetchServices () {
      //skip if list is not empty
      if (!this.isListEmpty) {
        console.info("service list not empty")
        return;
      }
      console.info("fetching services...")
      this.initUtils()
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

        let service_url = `${API_ENDPOINTS.root}/${service.thumbnail_url}`
        let thumb_url: string | null = null
        
        if (service_url) {
          thumb_url = await requests.getThumbnail(service_url)
          if (thumb_url) {
            this.thumbnails[service.id] = thumb_url
            return;
          }
        }
        //fallback to random pic
        thumb_url = await requests.requestRandomPictureUrl()
        console.log(thumb_url)
        if (thumb_url) {
          this.thumbnails[service.id] = thumb_url
          return;
        }
        this.thumbnails[service.id] = ''
      })
    },
    async fetchServiceById (serviceId: string) {

      this.initUtils()
      console.log(`fetching service ${serviceId}`)
      try {
        this.selectedService = await requests.requestServiceInfoById(serviceId)
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

      this.initUtils()
      try {
        this.lastResponse = await requests.requestOperationByServiceId(serviceId, payload)
      } catch (err) {
        this.errorMessageList.push(`Problem while making request to service '${serviceId}' :${err}`)
      } finally {
        this.loading = false
      }
    },
  },
})
