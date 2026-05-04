import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import IngredientList from '../../frontend/src/components/IngredientList.vue'

// Simulates a full HTML5 drag sequence: pick up fromIndex, drop on toIndex.
// jsdom lacks DragEvent and DataTransfer; Vue Test Utils' trigger() creates
// events internally and works correctly. The component guards against a
// missing dataTransfer so no error is thrown in the test environment.
async function simulateDrag(wrapper, fromIndex, toIndex) {
  const rows = () => wrapper.findAll('.ingredient-row')
  await rows()[fromIndex].trigger('dragstart')
  await rows()[toIndex].trigger('dragover')
  await rows()[toIndex].trigger('drop')
}

// Corrected factory that captures wrapper for the closure.
function mount_reactive(initialValue = []) {
  const wrapper = mount(IngredientList, {
    props: {
      modelValue: initialValue,
      'onUpdate:modelValue': (val) => wrapper.setProps({ modelValue: val }),
    },
  })
  return wrapper
}

function binLabels(wrapper) {
  return wrapper.findAll('.bin-label').map((el) => el.text())
}

function inputValues(wrapper) {
  return wrapper.findAll('input').map((el) => el.element.value)
}

// ---------------------------------------------------------------------------

describe('IngredientList — adding ingredients', () => {
  it('starts with no ingredient rows', () => {
    const wrapper = mount_reactive([])
    expect(wrapper.findAll('.ingredient-row')).toHaveLength(0)
  })

  it('adds a row when Add Ingredient is clicked', async () => {
    const wrapper = mount_reactive([])
    await wrapper.find('.btn-add').trigger('click')
    expect(wrapper.findAll('.ingredient-row')).toHaveLength(1)
  })

  it('shows sequential bin numbers as ingredients are added', async () => {
    const wrapper = mount_reactive([])
    const btn = wrapper.find('.btn-add')
    await btn.trigger('click')
    await btn.trigger('click')
    await btn.trigger('click')
    expect(binLabels(wrapper)).toEqual(['Bin 1', 'Bin 2', 'Bin 3'])
  })

  it('allows typing into an ingredient field', async () => {
    const wrapper = mount_reactive([])
    await wrapper.find('.btn-add').trigger('click')
    await wrapper.find('input').setValue('500g bread flour')
    expect(inputValues(wrapper)).toEqual(['500g bread flour'])
  })

  it('preserves other ingredients when one is updated', async () => {
    const wrapper = mount_reactive(['flour', 'water', 'salt'])
    await wrapper.findAll('input')[1].setValue('375g water')
    expect(inputValues(wrapper)).toEqual(['flour', '375g water', 'salt'])
  })
})

describe('IngredientList — removing ingredients', () => {
  it('removes an ingredient when the × button is clicked', async () => {
    const wrapper = mount_reactive(['flour', 'water', 'salt'])
    await wrapper.findAll('.btn-remove')[1].trigger('click')
    expect(inputValues(wrapper)).toEqual(['flour', 'salt'])
  })

  it('renumbers bins sequentially after a removal', async () => {
    const wrapper = mount_reactive(['flour', 'water', 'salt'])
    await wrapper.findAll('.btn-remove')[0].trigger('click')
    expect(binLabels(wrapper)).toEqual(['Bin 1', 'Bin 2'])
  })
})

describe('IngredientList — drag-and-drop reordering', () => {
  it('moves an ingredient when dragged to a new position', async () => {
    const wrapper = mount_reactive(['flour', 'water', 'salt'])
    await simulateDrag(wrapper, 0, 2)
    expect(inputValues(wrapper)).toEqual(['water', 'salt', 'flour'])
  })

  it('bin numbers always reflect the new visual order after a drag', async () => {
    const wrapper = mount_reactive(['flour', 'water', 'salt'])
    await simulateDrag(wrapper, 0, 2)
    // All three labels should still read Bin 1 / 2 / 3 — renumbered for the new order.
    expect(binLabels(wrapper)).toEqual(['Bin 1', 'Bin 2', 'Bin 3'])
  })

  it('dragging to the same position leaves the list unchanged', async () => {
    const wrapper = mount_reactive(['flour', 'water', 'salt'])
    await simulateDrag(wrapper, 1, 1)
    expect(inputValues(wrapper)).toEqual(['flour', 'water', 'salt'])
  })
})

describe('IngredientList — 20-ingredient limit', () => {
  it('disables the Add Ingredient button at 20 ingredients', () => {
    const full = Array.from({ length: 20 }, (_, i) => `Ingredient ${i + 1}`)
    const wrapper = mount_reactive(full)
    expect(wrapper.find('.btn-add').element.disabled).toBe(true)
  })

  it('shows the limit message at 20 ingredients', () => {
    const full = Array.from({ length: 20 }, (_, i) => `Ingredient ${i + 1}`)
    const wrapper = mount_reactive(full)
    expect(wrapper.find('.limit-note').exists()).toBe(true)
  })

  it('does not add a 21st ingredient when the button is clicked at the limit', async () => {
    const full = Array.from({ length: 20 }, (_, i) => `Ingredient ${i + 1}`)
    const wrapper = mount_reactive(full)
    await wrapper.find('.btn-add').trigger('click')
    expect(wrapper.findAll('.ingredient-row')).toHaveLength(20)
  })
})
