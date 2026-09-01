<script setup>
import { ref } from 'vue'
import axios from 'axios'

const demoTexts = [
  'I need 1.2 lakh rupees for a tailoring shop. My family earns 150000 a year.',
  'I want 3 lakh for a small dairy business. My income is 280000 annually.',
  'I need 5 lakh for a welding unit and earn 450000 per year.',
  'I am a college student and need 2 lakh for my engineering course. My family earns 300000 a year.'
]

const inputText = ref(demoTexts[0])
const results = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')

const useDemoInput = (text) => {
  inputText.value = text
  results.value = null
  errorMessage.value = ''
}

const submitApplication = async () => {
  if (!inputText.value.trim()) {
    errorMessage.value = 'Please enter a project description first.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await axios.post('http://127.0.0.1:8000/voice-apply', {
      translated_text: inputText.value,
      latitude: 26.144,
      longitude: 91.736
    })

    results.value = response.data
  } catch (error) {
    console.error('API Error:', error)
    errorMessage.value = 'The service is currently unavailable. Please try again in a moment.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-100 p-4 py-10 text-slate-800 sm:p-6">
    <div class="mx-auto max-w-5xl rounded-3xl border border-slate-200 bg-white shadow-xl">
      <header class="border-b border-slate-200 bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-500 px-6 py-8 text-white">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">MoSJE • Health-Aware Routing</p>
        <h1 class="mt-3 text-3xl font-bold">Scheme Matchmaker</h1>
        <p class="mt-2 text-sm text-blue-50">Voice-first vernacular eligibility and partner routing for marginalized entrepreneurs.</p>
      </header>

      <main class="grid gap-6 p-6 lg:grid-cols-[1.05fr_1.4fr]">
        <section class="rounded-2xl border border-slate-200 bg-slate-50 p-5">
          <label class="mb-2 block text-sm font-semibold text-slate-700">Describe your project</label>
          <textarea
            v-model="inputText"
            rows="6"
            class="w-full resize-none rounded-xl border border-slate-300 bg-white p-3 text-sm text-slate-700 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            placeholder="I need 1.2 lakh rupees for a tailoring shop. My family earns 150000 a year."
          ></textarea>

          <div class="mt-4 flex flex-wrap gap-2">
            <button
              v-for="demo in demoTexts"
              :key="demo"
              type="button"
              class="rounded-full border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:border-indigo-400 hover:text-indigo-700"
              @click="useDemoInput(demo)"
            >
              Demo case
            </button>
          </div>

          <button
            type="button"
            :disabled="isLoading"
            @click="submitApplication"
            class="mt-5 w-full rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-indigo-400"
          >
            {{ isLoading ? 'Checking eligibility...' : 'Find Eligible Schemes' }}
          </button>

          <p v-if="errorMessage" class="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {{ errorMessage }}
          </p>
        </section>

        <section class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div v-if="!results" class="flex h-full min-h-[280px] items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
            <div>
              <p class="text-lg font-semibold text-slate-700">Ready for demo</p>
              <p class="mt-2 text-sm text-slate-500">Enter a project description and click the button to simulate eligibility and routing.</p>
            </div>
          </div>

          <div v-else class="space-y-5">
            <div class="rounded-2xl border p-4" :class="results.simulation.is_eligible ? 'border-emerald-200 bg-emerald-50' : 'border-red-200 bg-red-50'">
              <p class="text-xs font-semibold uppercase tracking-[0.18em]" :class="results.simulation.is_eligible ? 'text-emerald-600' : 'text-red-600'">
                {{ results.simulation.is_eligible ? 'Eligible' : 'Not eligible' }}
              </p>
              <h2 class="mt-2 text-2xl font-bold text-slate-800">
                {{ results.simulation.is_eligible ? results.simulation.scheme_category : 'Application review needed' }}
              </h2>
              <p v-if="results.simulation.rejection_reason" class="mt-2 text-sm text-red-700">
                {{ results.simulation.rejection_reason }}
              </p>
            </div>

            <div class="grid gap-3 sm:grid-cols-2">
              <div class="rounded-xl bg-slate-50 p-3">
                <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Project cost</p>
                <p class="mt-1 text-lg font-bold text-slate-800">₹{{ results.simulation.total_project_cost }}</p>
              </div>
              <div class="rounded-xl bg-slate-50 p-3">
                <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Loan amount</p>
                <p class="mt-1 text-lg font-bold text-slate-800">₹{{ results.simulation.concessional_loan_amount }}</p>
              </div>
              <div class="rounded-xl bg-slate-50 p-3">
                <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Margin</p>
                <p class="mt-1 text-lg font-bold text-slate-800">₹{{ results.simulation.beneficiary_margin_money }}</p>
              </div>
              <div class="rounded-xl bg-slate-50 p-3">
                <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Moratorium</p>
                <p class="mt-1 text-lg font-bold text-slate-800">{{ results.simulation.moratorium_months }} months</p>
              </div>
            </div>

            <div>
              <h3 class="mb-3 text-lg font-semibold text-slate-800">
                Recommended partners ({{ results.recommended_partners.length }})
              </h3>
              <ul class="space-y-3">
                <li
                  v-for="partner in results.recommended_partners"
                  :key="partner.partner_id"
                  class="flex items-center justify-between rounded-xl border border-slate-200 p-3"
                >
                  <div>
                    <p class="font-semibold text-slate-800">{{ partner.name }}</p>
                    <p class="text-xs text-slate-500">{{ partner.type }} • {{ partner.distance_km }} km away</p>
                  </div>
                  <span
                    class="rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide"
                    :class="partner.health_status === 'Healthy' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'"
                  >
                    {{ partner.health_status }}
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>
