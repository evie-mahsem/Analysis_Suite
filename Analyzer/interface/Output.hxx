#ifndef __OUTPUT_HXX_
#define __OUTPUT_HXX_

template <class T>
size_t fillParticle(Particle& particle, int listName, T& fillObject, size_t idx, size_t pass_bitmap)
{
    size_t final_bitmap = particle.bitmap(listName).at(idx) & pass_bitmap;
    if (final_bitmap != 0) {
        fillObject.pt.push_back(particle.pt(idx));
        fillObject.eta.push_back(particle.eta(idx));
        fillObject.phi.push_back(particle.phi(idx));
        fillObject.mass.push_back(particle.mass(idx));
        fillObject.syst_bitMap.push_back(pass_bitmap);
    }
    return final_bitmap;
}

template <class T>
void fillParticle(Particle& particle, int listName, T& fillObject, size_t pass_bitmap)
{
    for (size_t idx = 0; idx < particle.size(); ++idx) {
        fillParticle(particle, listName, fillObject, idx, pass_bitmap);
    }
}

#endif // __OUTPUT_HXX_