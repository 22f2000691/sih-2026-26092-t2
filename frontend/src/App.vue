<script setup>
import { ref, onBeforeUnmount, computed, watch } from 'vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://sih-2026-26092-t2.onrender.com'

const demoTexts = [
  'I need 1.2 lakh rupees for a tailoring shop. My family earns 150000 a year.',
  'I want 3 lakh for a small dairy business. My income is 280000 annually.',
  'I need 5 lakh for a welding unit and earn 450000 per year.',
  'I am a college student and need 2 lakh for my engineering course. My family earns 300000 a year.'
]

const tabs = [
  { id: 'text', label: 'Text' },
  { id: 'voice', label: 'Voice' },
  { id: 'form', label: 'Form' }
]

const activeTab = ref('text')
const inputText = ref(demoTexts[0])
const results = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const isListening = ref(false)
const recognition = ref(null)

const formData = ref({
  amount: '3',
  unit: 'lakh',
  annualIncome: '300000',
  loanType: 'General',
  location: 'Assam'
})

const emiInputs = ref({
  principal: 0,
  rate: 7.5,
  tenure: 36,
  moratorium: 6
})

const emiSummary = computed(() => {
  const principal = Number(emiInputs.value.principal) || 0
  const annualRate = Number(emiInputs.value.rate) || 0
  const tenure = Number(emiInputs.value.tenure) || 1
  const moratorium = Number(emiInputs.value.moratorium) || 0

  const monthlyRate = annualRate / 12 / 100
  let emi = principal / tenure

  if (monthlyRate > 0) {
    const factor = Math.pow(1 + monthlyRate, tenure)
    emi = (principal * monthlyRate * factor) / (factor - 1)
  }

  const totalPayable = emi * tenure
  const totalInterest = totalPayable - principal

  return {
    principal,
    annualRate,
    tenure,
    moratorium,
    emi,
    totalPayable,
    totalInterest,
    postMoratoriumNote: moratorium > 0 ? `Moratorium of ${moratorium} months before standard EMI starts.` : 'No moratorium applied.'
  }
})

watch(
  () => results.value,
  (newResults) => {
    if (!newResults?.simulation) return

    const loanValue = Number(newResults.simulation.concessional_loan_amount || 0)
    const rateValue = Number(newResults.simulation.interest_rate || 7.5)
    const moratoriumValue = Number(newResults.simulation.moratorium_months || 6)

    emiInputs.value = {
      principal: loanValue,
      rate: rateValue,
      tenure: 36,
      moratorium: moratoriumValue
    }
  },
  { immediate: true }
)

const resetResultState = () => {
  results.value = null
  errorMessage.value = ''
}

const useDemoInput = (text) => {
  activeTab.value = 'text'
  inputText.value = text
  resetResultState()
}

const buildFormText = () => {
  const parsedAmount = Number(formData.value.amount) || 0
  const amountText = `${parsedAmount} ${formData.value.unit}`
  const loanType = formData.value.loanType || 'General'
  const incomeText = `My annual income is ${formData.value.annualIncome || '300000'} rupees.`

  if (loanType === 'Education') {
    return `I need ${amountText} for my education loan. I am a student. ${incomeText}`
  }

  return `I need ${amountText} for my ${loanType.toLowerCase()} business. ${incomeText}`
}

const startVoiceCapture = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

  if (!SpeechRecognition) {
    errorMessage.value = 'Voice input is not supported in this browser. Please use text or form mode.'
    return
  }

  if (recognition.value) {
    recognition.value.stop()
  }

  const recognitionInstance = new SpeechRecognition()
  recognitionInstance.lang = 'en-IN'
  recognitionInstance.interimResults = false
  recognitionInstance.maxAlternatives = 1

  recognitionInstance.onstart = () => {
    isListening.value = true
    errorMessage.value = ''
  }

  recognitionInstance.onresult = (event) => {
    const transcript = event.results[0][0].transcript
    inputText.value = transcript
    activeTab.value = 'voice'
    resetResultState()
  }

  recognitionInstance.onerror = () => {
    errorMessage.value = 'Voice capture failed. Please try again or switch to text mode.'
  }

  recognitionInstance.onend = () => {
    isListening.value = false
  }

  recognition.value = recognitionInstance
  recognitionInstance.start()
}

const stopVoiceCapture = () => {
  recognition.value?.stop()
  isListening.value = false
}

const submitApplication = async () => {
  const textToSubmit = activeTab.value === 'form' ? buildFormText() : inputText.value

  if (!textToSubmit.trim() && activeTab.value !== 'form') {
    errorMessage.value = 'Please enter a project description first.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const payload = activeTab.value === 'form'
      ? {
          input_mode: 'form',
          loan_type: formData.value.loanType,
          capital_required: Number(formData.value.amount) * (
            formData.value.unit === 'lakh' ? 100000 :
            formData.value.unit === 'crore' ? 10000000 :
            formData.value.unit === 'thousand' ? 1000 : 1
          ),
          annual_income: Number(formData.value.annualIncome) || 0,
          latitude: 26.144,
          longitude: 91.736
        }
      : {
          input_mode: activeTab.value,
          translated_text: textToSubmit,
          latitude: 26.144,
          longitude: 91.736
        }

    const response = await axios.post(`${API_BASE_URL}/apply`, payload)
    results.value = response.data
  } catch (error) {
    console.error('API Error:', error)
    const serverMessage = error?.response?.data?.detail || error?.response?.data?.message || error?.message || 'Unknown server error'
    errorMessage.value = `The service is currently unavailable. ${serverMessage}`
  } finally {
    isLoading.value = false
  }
}

onBeforeUnmount(() => {
  stopVoiceCapture()
})
</script>

<template>
  <div class="min-h-screen bg-slate-100 p-4 py-10 text-slate-800 sm:p-6">
    <div class="mx-auto max-w-5xl rounded-3xl border border-slate-200 bg-white shadow-xl">
      <header class="border-b border-slate-200 bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-500 px-6 py-8 text-white">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">MoSJE • Health-Aware Routing</p>
        <h1 class="mt-3 text-3xl font-bold">Scheme Matchmaker</h1>
        <p class="mt-2 text-sm text-blue-50">Flexible input modes for vernacular loan discovery and partner routing.</p>
      </header>

      <main class="grid gap-6 p-6 lg:grid-cols-[1.05fr_1.4fr]">
        <section class="rounded-2xl border border-slate-200 bg-slate-50 p-5">
          <div class="mb-4 flex gap-2 rounded-xl bg-slate-200 p-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              type="button"
              class="flex-1 rounded-lg px-3 py-2 text-sm font-semibold transition"
              :class="activeTab === tab.id ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-600 hover:text-slate-800'"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <div class="mb-4 rounded-xl border border-indigo-100 bg-indigo-50 px-3 py-2 text-xs text-indigo-700">
            Choose the quickest input mode for your applicant profile.
          </div>

          <div v-if="activeTab === 'text'" class="space-y-3">
            <label class="block text-sm font-semibold text-slate-700">Project description</label>
            <textarea
              v-model="inputText"
              rows="6"
              class="w-full resize-none rounded-xl border border-slate-300 bg-white p-3 text-sm text-slate-700 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="I need 1.2 lakh rupees for a tailoring shop. My family earns 150000 a year."
            ></textarea>
          </div>

          <div v-else-if="activeTab === 'voice'" class="space-y-4">
            <label class="block text-sm font-semibold text-slate-700">Voice input</label>
            <div class="rounded-xl border border-dashed border-slate-300 bg-white p-4">
              <p class="text-sm text-slate-600">Click the mic and speak naturally. The transcript will populate here.</p>
              <button
                type="button"
                @click="isListening ? stopVoiceCapture() : startVoiceCapture()"
                class="mt-4 inline-flex items-center rounded-xl px-4 py-2 text-sm font-semibold transition"
                :class="isListening ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-indigo-600 text-white hover:bg-indigo-700'"
              >
                {{ isListening ? 'Stop listening' : 'Use microphone' }}
              </button>
            </div>

            <textarea
              v-model="inputText"
              rows="5"
              class="w-full resize-none rounded-xl border border-slate-300 bg-white p-3 text-sm text-slate-700 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Your spoken transcript appears here..."
            ></textarea>
          </div>

          <div v-else class="space-y-4">
            <div class="grid gap-3 sm:grid-cols-2">
              <div>
                <label class="mb-1 block text-sm font-medium text-slate-700">Loan amount</label>
                <input v-model="formData.amount" type="number" min="0" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700" />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-slate-700">Unit</label>
                <select v-model="formData.unit" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700">
                  <option value="lakh">Lakh</option>
                  <option value="crore">Crore</option>
                  <option value="thousand">Thousand</option>
                  <option value="rupees">Rupees</option>
                </select>
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-slate-700">Annual income</label>
                <input v-model="formData.annualIncome" type="number" min="0" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700" />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium text-slate-700">Loan type</label>
                <select v-model="formData.loanType" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700">
                  <option value="General">General</option>
                  <option value="Tailoring">Tailoring</option>
                  <option value="Dairy">Dairy</option>
                  <option value="Welding">Welding</option>
                  <option value="Farming">Farming</option>
                  <option value="Education">Education</option>
                </select>
              </div>
            </div>

            <div class="rounded-xl border border-slate-200 bg-white p-3">
              <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Generated prompt</p>
              <p class="mt-2 text-sm text-slate-700">{{ buildFormText() }}</p>
            </div>
          </div>

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
              <p class="text-lg font-semibold text-slate-700">Demo output</p>
              <p class="mt-2 text-sm text-slate-500">Use text, voice, or form mode and submit to simulate eligibility and routing.</p>
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

            <div class="rounded-2xl border border-blue-200 bg-blue-50 p-4">
              <h3 class="mb-3 text-lg font-semibold text-slate-800">Financial calculator</h3>

              <div class="grid gap-3 sm:grid-cols-2">
                <div>
                  <label class="mb-1 block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Principal</label>
                  <input v-model.number="emiInputs.principal" type="number" min="0" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700" />
                </div>
                <div>
                  <label class="mb-1 block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Rate %</label>
                  <input v-model.number="emiInputs.rate" type="number" min="0" step="0.1" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700" />
                </div>
                <div>
                  <label class="mb-1 block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Tenure (months)</label>
                  <input v-model.number="emiInputs.tenure" type="number" min="1" step="1" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700" />
                </div>
                <div>
                  <label class="mb-1 block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Moratorium (months)</label>
                  <input v-model.number="emiInputs.moratorium" type="number" min="0" step="1" class="w-full rounded-xl border border-slate-300 bg-white p-2.5 text-sm text-slate-700" />
                </div>
              </div>

              <div class="mt-4 rounded-xl bg-white p-3">
                <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Projected EMI</p>
                <p class="mt-2 text-2xl font-bold text-slate-800">₹{{ emiSummary.emi.toFixed(0) }}</p>
                <p class="mt-2 text-xs text-slate-600">{{ emiSummary.postMoratoriumNote }}</p>
              </div>

              <div class="mt-4 grid gap-3 sm:grid-cols-3">
                <div class="rounded-xl bg-white p-3">
                  <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Total payable</p>
                  <p class="mt-1 text-lg font-bold text-slate-800">₹{{ emiSummary.totalPayable.toFixed(0) }}</p>
                </div>
                <div class="rounded-xl bg-white p-3">
                  <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Interest</p>
                  <p class="mt-1 text-lg font-bold text-slate-800">₹{{ emiSummary.totalInterest.toFixed(0) }}</p>
                </div>
                <div class="rounded-xl bg-white p-3">
                  <p class="text-xs uppercase tracking-[0.16em] text-slate-500">Rate</p>
                  <p class="mt-1 text-lg font-bold text-slate-800">{{ emiSummary.annualRate }}%</p>
                </div>
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
