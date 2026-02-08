<template>
  <div class="min-h-screen p-4 md:p-8 flex flex-col md:flex-row gap-6">
    <!-- Left Panel: Input -->
    <div class="w-full md:w-1/3 bg-white/80 backdrop-blur-md rounded-3xl shadow-xl p-6 border border-white/50 flex flex-col gap-6 h-fit sticky top-8">
      <h1 class="text-3xl font-bold text-primary mb-2">ComicGen 🎨</h1>
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-bold mb-2">主角 (Character)</label>
          <input 
            v-model="character" 
            class="w-full p-4 rounded-xl bg-background border border-pink-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all"
            placeholder="Ex: A brave little toaster..."
          />
        </div>
        
        <div>
          <label class="block text-sm font-bold mb-2">页数 (Page Count)</label>
          <input 
            v-model.number="pageCount" 
            type="number"
            min="1"
            max="10"
            class="w-full p-4 rounded-xl bg-background border border-pink-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all"
            placeholder="3"
          />
        </div>
        
        <div>
          <label class="block text-sm font-bold mb-2">故事情节 (Plot)</label>
          <textarea 
            v-model="plot" 
            class="w-full p-4 rounded-xl bg-background border border-pink-200 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all h-40 resize-none"
            placeholder="Ex: Goes on an adventure to find the perfect slice of bread..."
          ></textarea>
        </div>
        
        <button 
          @click="generateStory" 
          :disabled="loadingStory || !character || !plot"
          class="w-full py-4 rounded-xl bg-gradient-to-r from-primary to-secondary text-white font-bold text-lg shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loadingStory" class="animate-pulse">Generating Story... ✨</span>
          <span v-else>Generate Story 🚀</span>
        </button>
      </div>
    </div>

    <!-- Right Panel: Output -->
    <div class="w-full md:w-2/3 space-y-6">
      <div v-if="!story && !loadingStory" class="h-full flex items-center justify-center opacity-50">
        <div class="text-center">
          <p class="text-2xl">Ready to create magic?</p>
          <p>Fill in the details and start your journey!</p>
        </div>
      </div>

      <div v-if="story" class="space-y-8 animate-fade-in">
        <header class="bg-white/90 backdrop-blur rounded-2xl p-6 shadow-sm border border-pink-100 flex flex-col gap-4">
          <div class="flex justify-between items-center">
            <h2 class="text-2xl font-bold text-text">{{ story.title }}</h2>
            <button 
              v-if="hasImages" 
              @click="downloadAll"
              class="px-6 py-2 rounded-full bg-cta text-white font-bold hover:bg-cyan-600 transition-colors shadow-md flex items-center gap-2"
            >
              <span>Download ZIP 📦</span>
            </button>
            <button 
              v-if="hasImages" 
              @click="downloadLongImage"
              class="px-6 py-2 rounded-full bg-pink-500 text-white font-bold hover:bg-pink-600 transition-colors shadow-md flex items-center gap-2"
            >
              <span>Download Long Image 📜</span>
            </button>
          </div>
          
          <!-- Character Design Section -->
          <div v-if="story.character_design" class="bg-pink-50 p-4 rounded-xl border border-pink-100">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-lg">👤</span>
              <span class="font-bold text-primary">Character Design</span>
            </div>
            <p class="text-sm text-gray-700 leading-relaxed">{{ story.character_design }}</p>
            <p class="text-xs text-gray-400 mt-2 italic">* This design will be applied to all generated images.</p>
          </div>
        </header>

        <div class="grid grid-cols-1 gap-8">
          <div 
            v-for="(page, index) in story.pages" 
            :key="index"
            class="bg-white rounded-3xl overflow-hidden shadow-lg border border-pink-100 hover:shadow-xl transition-shadow duration-300"
          >
            <div class="flex flex-col md:flex-row">
              <!-- Prompt & Details -->
              <div class="p-6 md:w-1/2 flex flex-col justify-between space-y-4 max-h-[600px] overflow-y-auto">
                <div>
                  <div class="flex items-center gap-2 mb-3">
                    <span class="bg-pink-100 text-primary px-3 py-1 rounded-full text-xs font-bold">Page {{ index + 1 }}</span>
                    <span class="text-gray-400 text-xs font-medium">{{ page.panels.length }} Panels</span>
                  </div>
                  
                  <!-- Panels List -->
                  <div class="space-y-4">
                    <div v-for="panel in page.panels" :key="panel.panel_number" class="border-b border-gray-100 pb-4 last:border-0">
                      <div class="flex items-center gap-2 mb-2">
                        <span class="w-6 h-6 flex items-center justify-center bg-gray-100 rounded-full text-xs font-bold text-gray-500">{{ panel.panel_number }}</span>
                        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Description</span>
                      </div>
                      <p class="text-sm leading-relaxed text-gray-700 font-medium mb-2 pl-8">{{ panel.text }}</p>

                      <!-- Dialogue -->
                      <div v-if="panel.dialogue" class="ml-8 mb-2 bg-pink-50/50 p-3 rounded-xl border border-pink-100">
                        <span class="text-xs font-bold text-pink-400 uppercase tracking-wider block mb-1">Dialogue</span>
                        <p class="text-sm text-gray-800 italic">"{{ panel.dialogue }}"</p>
                      </div>
                      
                      <!-- Technical Details -->
                      <div class="ml-8 grid grid-cols-2 gap-2 text-xs text-gray-500 bg-gray-50 p-2 rounded-lg">
                        <div v-if="panel.scene" class="flex items-center gap-1">
                          <span>🎬</span>
                          <span>{{ panel.scene }}</span>
                        </div>
                        <div v-if="panel.shot" class="flex items-center gap-1">
                          <span>🎥</span>
                          <span>{{ panel.shot }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <button 
                  @click="generateImage(index, page.prompt)" 
                  :disabled="generatingImages[index]"
                  class="mt-4 w-full py-3 rounded-xl border-2 border-primary text-primary font-bold hover:bg-primary hover:text-white transition-all flex items-center justify-center gap-2 sticky bottom-0 bg-white shadow-up"
                >
                  <span v-if="generatingImages[index]" class="animate-spin">⚡</span>
                  <span>{{ images[index] ? 'Regenerate Page' : 'Generate Page' }}</span>
                </button>
              </div>

              <!-- Image Result -->
              <div class="md:w-1/2 bg-gray-50 min-h-[400px] flex items-center justify-center relative group border-l border-pink-50">
                <div v-if="generatingImages[index]" class="absolute inset-0 flex items-center justify-center bg-white/50 backdrop-blur-sm z-10">
                  <div class="animate-bounce text-4xl">🎨</div>
                </div>
                
                <img 
                  v-if="images[index]" 
                  :src="`data:image/png;base64,${images[index]}`" 
                  class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-105 cursor-pointer"
                  @click="openPreview(images[index])"
                />
                <div v-else class="text-gray-300 text-center p-8">
                  <div class="text-4xl mb-2">📄</div>
                  <p class="text-sm">Page layout will appear here</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import JSZip from 'jszip'
import { saveAs } from 'file-saver'

const character = ref('')
const plot = ref('')
const pageCount = ref(3)
const story = ref(null)
const loadingStory = ref(false)
const generatingImages = ref({})
const images = ref({})

const hasImages = computed(() => Object.keys(images.value).length > 0)

const generateStory = async () => {
  loadingStory.value = true
  story.value = null
  images.value = {}
  
  try {
    const response = await axios.post('/api/story', {
      character: character.value,
      plot: plot.value,
      page_count: pageCount.value
    })
    story.value = response.data
    // Normalize pages if structure differs
    if (!story.value.pages && Array.isArray(story.value)) {
        // Handle case where root is array or different structure
    }
  } catch (error) {
    console.error(error)
    alert('Failed to generate story. Please try again.')
  } finally {
    loadingStory.value = false
  }
}

const generateImage = async (index, prompt) => {
  generatingImages.value = { ...generatingImages.value, [index]: true }
  
  try {
    const response = await axios.post('/api/image', {
      prompt: prompt,
      page_number: index + 1,
      story_title: story.value.title,
      character_design: story.value.character_design
    })
    images.value = { ...images.value, [index]: response.data.image_data }
  } catch (error) {
    console.error(error)
    alert('Failed to generate image.')
  } finally {
    generatingImages.value = { ...generatingImages.value, [index]: false }
  }
}

const downloadAll = async () => {
  const zip = new JSZip()
  const folder = zip.folder(story.value.title || 'comic')
  
  for (const [index, base64Data] of Object.entries(images.value)) {
    folder.file(`page_${Number(index) + 1}.png`, base64Data, { base64: true })
  }
  
  const content = await zip.generateAsync({ type: 'blob' })
  saveAs(content, `${story.value.title || 'comic'}.zip`)
}

const downloadLongImage = async () => {
  if (!hasImages.value) return
  
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  // Load all images first to get dimensions
  const imageElements = []
  let totalHeight = 0
  let maxWidth = 0
  
  // Sort keys to ensure correct order
  const sortedIndices = Object.keys(images.value).sort((a, b) => Number(a) - Number(b))
  
  for (const index of sortedIndices) {
    const img = new Image()
    img.src = `data:image/png;base64,${images.value[index]}`
    await new Promise(resolve => {
      img.onload = () => {
        imageElements.push(img)
        totalHeight += img.height
        maxWidth = Math.max(maxWidth, img.width)
        resolve()
      }
    })
  }
  
  // Set canvas dimensions
  canvas.width = maxWidth
  canvas.height = totalHeight
  
  // Draw images
  let currentY = 0
  for (const img of imageElements) {
    ctx.drawImage(img, 0, currentY)
    currentY += img.height
  }
  
  // Export and download
  canvas.toBlob((blob) => {
    saveAs(blob, `${story.value.title || 'comic'}_long.png`)
  })
}

const openPreview = (base64) => {
    // Optional: open in modal
}
</script>

<style>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
