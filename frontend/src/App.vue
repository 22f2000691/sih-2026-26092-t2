<script setup>
import { ref } from 'vue'
import axios from 'axios'

const inputText = ref('')
const results = ref(null)
const isLoading = ref(false)

const submitApplication = async () => {
  if (!inputText.value) return
  isLoading.value = true
  
  try {
    const response = await axios.post('http://127.0.0.1:8000/voice-apply', {
      translated_text: inputText.value,
      latitude: 26.1440,
      longitude: 91.7360
    })
    results.value = response.data
  } catch (error) {
    console.error("API Error:", error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen p-6 flex flex-col items-center justify-center">
    <div class="w-full max-w-md bg-white rounded-xl shadow-lg p-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-2">Scheme Matchmaker</h1>
      <p class="text-gray-500 mb-6 text-sm">Voice-first vernacular routing</p>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">Describe your project (Text/Voice Simulation)</label>
        <textarea 
          v-model="inputText" 
          rows="3"
          class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
          placeholder="e.g., I need 1.2 lakh rupees for a tailoring shop. My family earns 150000 a year."
        ></textarea>
      </div>

      <button 
        @click="submitApplication" 
        :disabled="isLoading"
        class="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
      >
        {{ isLoading ? 'Processing...' : 'Find Eligible Schemes' }}
      </button>

      <div v-if="results" class="mt-6 border-t pt-4">
        <h2 class="text-lg font-semibold text-green-700 mb-2">
          {{ results.simulation.is_eligible ? 'Eligible: ' + results.simulation.scheme_category : 'Not Eligible' }}
        </h2>
        
        <div class="bg-gray-50 rounded-lg p-3 text-sm text-gray-700 mb-4 font-mono">
          <p>Project Cost: ₹{{ results.simulation.total_project_cost }}</p>
          <p>Loan (90%): ₹{{ results.simulation.concessional_loan_amount }} @ {{ results.simulation.interest_rate }}%</p>
          <p>Margin (10%): ₹{{ results.simulation.beneficiary_margin_money }}</p>
          <p>Moratorium: {{ results.simulation.moratorium_months }} Months</p>
        </div>

        <h3 class="font-semibold text-gray-800 mb-2">Recommended Partners ({{ results.recommended_partners.length }})</h3>
        <ul class="space-y-2">
          <li v-for="partner in results.recommended_partners" :key="partner.partner_id" class="p-3 border rounded-lg flex justify-between items-center">
            <div>
              <p class="font-medium text-sm">{{ partner.name }}</p>
              <p class="text-xs text-gray-500">{{ partner.type }} • {{ partner.distance_km }} km away</p>
            </div>
            <span :class="partner.health_status === 'Healthy' ? 'text-green-600' : 'text-yellow-600'" class="text-xs font-bold uppercase">
              {{ partner.health_status }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
