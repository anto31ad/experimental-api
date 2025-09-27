import { defineStore } from 'pinia'
import { requests } from '../utils/requests'

export interface ServiceParameter {
  name: string,
  description: string,
  examples?: Array<JSON>
}

export interface Service {
  id: string,
  name?: string,
  description?: string,
  thumbnail_url?: string,
  alt_thumbnail_url?: string,
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
    getServiceById: (state) => (id: string) => {
      return state.services.find(service => (service.id === id))
    },
    findServiceIndex: (state) => (id: string) => {
      return state.services.findIndex(service => (service.id === id))
    },
    hasErrors: (state) => state.errorMessageList.length > 0,
  },
  actions: {
    resetServiceRequestState() {
      this.loading = true
      this.errorMessageList = []
      console.log("reset service request state")
    },

    async fetchServices () {
      console.info("fetching services...")
      try {
        const serviceIdList = await requests.requestListOfServices()

        for (const id of serviceIdList) {
          // only fetch the details of service if they had not been already fetched  
          let index = this.findServiceIndex(id)
          if (index >= 0) {
            console.info("service already fetched", id)
            continue;
          }
          await this.fetchServiceById(id)
          this.fetchServiceThumbnail(id)
        }
      } catch (err) {
        this.errorMessageList.push('Failed to fetch services: ' + err)
      } finally {
        this.loading = false
      }
    },
    async fetchServiceThumbnail(serviceId: string) {

      const service = this.services[this.findServiceIndex(serviceId)]
      if (!service) {
        console.error("Not valid index")
        return;
      }

      let thumb_url: string | null = null
      if (service.thumbnail_url) {
        thumb_url = await requests.getThumbnail(service.thumbnail_url)
        if (thumb_url) {
          return;
        }
      }
      service.thumbnail_url = undefined
      //fallback to random pic
      thumb_url = await requests.requestRandomPictureUrl()
      console.log(thumb_url)
      if (thumb_url) {
        service.alt_thumbnail_url = thumb_url
        return;
      }
      service.alt_thumbnail_url = undefined
    },
    async selectService(serviceId: string) {
      this.selectedServiceId = serviceId
      this.fetchServiceById(serviceId)
    },
    async fetchServiceById (serviceId: string) {
      try {
        this.resetServiceRequestState()
        console.log(`fetching service ${serviceId}`)
        const serviceInfo = await requests.requestServiceInfoById(serviceId)

        const index = this.findServiceIndex(serviceId)
        if (index >= 0) {
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
        console.log(`Make Request to servie ${serviceId}`, payload)
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
