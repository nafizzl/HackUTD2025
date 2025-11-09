import { defineStore } from 'pinia'

// Mock car data
const carData = [
  {
    id: 1,
    make: 'Toyota',
    model: 'RAV4 Hybrid',
    year: 2025,
    price: 34500,
    description: 'The perfect blend of SUV capability and hybrid efficiency. Ready for any adventure.',
    features: ['Heated Seats', 'Apple CarPlay', 'AWD'],
    img: 'https://www.toyota.com/imgix/responsive/images/gallery/photos-videos/2025/rav4hybrid/xse/RAV_MY25_0010_V001_1.png?w=1600&h=900&q=90&fm=png&fit=max&cs=strip&bg=transparent'
  },
  {
    id: 2,
    make: 'Toyota',
    model: 'Prius',
    year: 2025,
    price: 31200,
    description: 'The iconic hybrid, redesigned with stunning style and unbeatable fuel economy.',
    features: ['Heated Seats', 'Apple CarPlay', 'Push to Start'],
    img: 'https://www.toyota.com/imgix/responsive/images/gallery/photos-videos/2025/prius/le/PRI_MY25_0002_V001_1.png?w=1600&h=900&q=90&fm=png&fit=max&cs=strip&bg=transparent'
  },
  {
    id: 3,
    make: 'Toyota',
    model: 'Tacoma',
    year: 2025,
    price: 38900,
    description: 'The legendary off-road truck, tougher and more capable than ever before.',
    features: ['Apple CarPlay', 'Push to Start', 'AWD'],
    img: 'https://www.toyota.com/imgix/responsive/images/gallery/photos-videos/2024/tacoma/trd_offroad/TAC_MY24_0009_V001.png?w=1600&h=900&q=90&fm=png&fit=max&cs=strip&bg=transparent'
  }
]

export const useCarStore = defineStore('carStore', {
  state: () => ({
    budget: 450,
    mustHaves: {
      heatedSeats: false,
      pushToStart: false,
      appleCarPlay: false,
      awd: false
    },
    allCars: carData,
    likedCars: [],
    // We just need to track the IDs of seen cars
    seenCarIds: new Set()
  }),

  getters: {
    // This creates the swipe deck for you!
    carsForSwiping: (state) => {
      return state.allCars.filter(car => {
        // 1. Haven't we seen it yet?
        if (state.seenCarIds.has(car.id)) {
          return false
        }
        
        // 2. Check budget (simple estimate: price / 72-month loan)
        if ((car.price / 72) > state.budget) {
          return false
        }

        // 3. Check must-haves
        if (state.mustHaves.heatedSeats && !car.features.includes('Heated Seats')) {
          return false
        }
        if (state.mustHaves.pushToStart && !car.features.includes('Push to Start')) {
          return false
        }
        if (state.mustHaves.appleCarPlay && !car.features.includes('Apple CarPlay')) {
          return false
        }
        if (state.mustHaves.awd && !car.features.includes('AWD')) {
          return false
        }

        return true // If it passes all checks, show it!
      })
    }
  },

  actions: {
    setBudget(newBudget) {
      this.budget = newBudget
    },
    toggleMustHave(feature) {
      this.mustHaves[feature] = !this.mustHaves[feature]
    },
    // Actions now take the car object, which is cleaner
    likeCar(car) {
      this.likedCars.push(car)
      this.seenCarIds.add(car.id)
    },
    nopeCar(car) {
      this.seenCarIds.add(car.id)
    },
    getCarById(id) {
      return this.allCars.find(car => car.id === id)
    }
  }
})